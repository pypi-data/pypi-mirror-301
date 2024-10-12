# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 08:29:02 2020

@author: Guy McBride

"""

import sys
import os
import logging
from dataclasses import dataclass, field
from collections import deque
from typing import List

import keysight_tse as kthvi


log = logging.getLogger(__name__)

# Cached record of modules that are used in the HVI.
modules = None
system_definition = None
sequencer = None
current_sync_sequence = deque()
current_block = deque()
hvi_handle = None


@dataclass
class ModuleDescriptor:
    """Holds a 'description' of a used module"""

    name: str
    input_triggers: List[str] = field(default_factory=list)
    output_triggers: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    triggerActionMap: dict = field(default_factory=dict)
    eventTriggerMap: dict = field(default_factory=dict)
    fpgaRegisterMap: dict = field(default_factory=dict)
    hvi_registers: List[str] = field(default_factory=list)
    fpga: str = None
    handle: int = None
    _current_sequence = None


def define_system(name: str, **kwargs):
    global modules, system_definition, sequencer, current_sync_sequence
    pxi_triggers = [trigger for trigger in range(8)]

    defaultKwargs = {
        "chassis_list": [1],
        "pxi_triggers": pxi_triggers,
        "modules": [],
        "simulate": False,
    }
    kwargs = {**defaultKwargs, **kwargs}
    modules = kwargs["modules"]

    system_definition = kthvi.SystemDefinition(name)
    for chassis in kwargs["chassis_list"]:
        if kwargs["simulate"]:
            system_definition.chassis.add_with_options(
                chassis, "Simulate=True,DriverSetup=model=GenericChassis"
            )
        else:
            system_definition.chassis.add(chassis)

    # Add PXI trigger resources that we plan to use
    log.info("Adding PXIe triggers to the HVI environment...")
    pxiTriggers = []
    for trigger in kwargs["pxi_triggers"]:
        pxiTriggerName = "PXI_TRIGGER{}".format(trigger)
        pxiTrigger = getattr(kthvi.TriggerResourceId, pxiTriggerName)
        pxiTriggers.append(pxiTrigger)
    system_definition.sync_resources = pxiTriggers

    log.info("Adding modules to the HVI environment...")
    for module in kwargs["modules"]:
        module._current_sequence = deque()
        system_definition.engines.add(
            module.handle.hvi.engines.main_engine, module.name
        )
        log.info(f"...Declaring Input Triggers used by: {module.name}...")
        if module.input_triggers is not None:
            for trigger in module.input_triggers:
                log.info(f"...adding: {trigger}")
                trigger_id = getattr(module.handle.hvi.triggers, trigger)
                system_definition.engines[module.name].triggers.add(trigger_id, trigger)

        log.info(f"...Declaring Output Triggers used by: {module.name}...")
        if module.output_triggers is not None:
            for trigger in module.output_triggers:
                log.info(f"...adding: {trigger}")
                trigger_id = getattr(module.handle.hvi.triggers, trigger)
                system_definition.engines[module.name].triggers.add(trigger_id, trigger)
                system_definition.engines[module.name].triggers[
                    trigger
                ].config.direction = kthvi.Direction.OUTPUT
                system_definition.engines[module.name].triggers[
                    trigger
                ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
                system_definition.engines[module.name].triggers[
                    trigger
                ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
                system_definition.engines[module.name].triggers[
                    trigger
                ].config.hw_routing_delay = 0
                system_definition.engines[module.name].triggers[
                    trigger
                ].config.trigger_mode = kthvi.TriggerMode.LEVEL

        log.info(f"...Declaring actions used by: {module.name}...")
        if module.actions is not None:
            if len(module.actions) == 0:
                actions = [
                    a for a in dir(module.handle.hvi.actions) if not a.startswith("_")
                ]
                module.actions = actions
            else:
                actions = module.actions
            for action in actions:
                log.info(f"...adding: {action}")
                action_id = getattr(module.handle.hvi.actions, action)
                system_definition.engines[module.name].actions.add(action_id, action)

        log.info(f"...Declaring events used by: {module.name}...")
        if module.events is not None:
            if len(module.events) == 0:
                events = [
                    e for e in dir(module.handle.hvi.events) if not e.startswith("_")
                ]
                module.events = events
            else:
                events = module.events
            for event in events:
                log.info(f"...adding: {event}")
                event_id = getattr(module.handle.hvi.events, event)
                system_definition.engines[module.name].events.add(event_id, event)

        log.info(f"...Mapping triggers to actions on: {module.name}...")
        if module.triggerActionMap is not None:
            for mapping in module.triggerActionMap.items():
                log.info(f"...connecting: {mapping[0]} -> (Action){mapping[1]}")
                # Register trigger as an event so HVI knows about it
                trigger_id = getattr(module.handle.hvi.triggers, mapping[0])
                triggerEvent = system_definition.engines[module.name].events.add(
                    trigger_id, mapping[0]
                )
                # Set up the characteristics of the physical trigger
                trigger = system_definition.engines[module.name].triggers[mapping[0]]
                trigger.config.direction = kthvi.Direction.INPUT
                trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                trigger.config.hw_routing_delay = 0
                trigger.config.trigger_mode = kthvi.TriggerMode.PULSE
                # Finally connect the trigger to the action input to the sandbox
                action_id = getattr(module.handle.hvi.actions, mapping[1])
                triggerAction = system_definition.engines[module.name].actions[
                    mapping[1]
                ]
                triggerAction.config.source = triggerEvent
                triggerAction.config.sync_mode = kthvi.SyncMode.IMMEDIATE

        log.info(f"...Mapping events to triggers on: {module.name}...")
        if module.triggerActionMap is not None:
            for mapping in module.eventTriggerMap.items():
                log.info(f"...connecting: (Event){mapping[0]} -> {mapping[1]}")
                # Set up the characteristics of the physical trigger
                trigger_id = getattr(module.handle.hvi.triggers, mapping[1])
                trigger = system_definition.engines[module.name].triggers[mapping[1]]
                trigger.config.direction = kthvi.Direction.OUTPUT
                trigger.config.polarity = kthvi.Polarity.ACTIVE_HIGH
                trigger.config.sync_mode = kthvi.SyncMode.IMMEDIATE
                trigger.config.hw_routing_delay = 0
                trigger.config.trigger_mode = kthvi.TriggerMode.LEVEL
                # Connect the event output of the sandbox to the physical trigger
                source_event = system_definition.engines[module.name].events[mapping[0]]
                trigger.config.source = source_event

        if module.fpga:
            log.info(f"...Declaring FPGA Registers used by: {module.name}...")
            sandbox = system_definition.engines[module.name].fpga_sandboxes[0]
            try:
                sandbox.load_from_k7z(
                    os.getcwd() + "\\" + module.fpga
                )
                log.info(f"FDS ports: {sandbox.fds_ports.count}")
                for register in (
                    system_definition.engines[module.name].fpga_sandboxes[0].fds_ports
                ):
                    log.info(f"...... {register.name}")
                log.info(f"Registers: {sandbox.fpga_registers.count}")
                for register in (
                    system_definition.engines[module.name].fpga_sandboxes[0].fpga_registers
                ):
                    log.info(f"...... {register.name}")
                log.info(f"Memory Banks: {sandbox.fpga_memory_maps.count}")
                for register in (
                    system_definition.engines[module.name].fpga_sandboxes[0].fpga_memory_maps
                ):
                    log.info(f"...... {register.name}")
            except Exception as err:
                if err.args[0] == "No interface named 'MainEngine_Memory'":
                    log.info("No HVI registers")
                else:
                    raise err

    log.info("Creating Main Sequencer Block...")
    sequencer = kthvi.Sequencer(f"{name}_Sequencer", system_definition)
    current_sync_sequence.append(sequencer.sync_sequence)

    log.info("Declaring HVI registers...")
    scopes = sequencer.sync_sequence.scopes
    for module in kwargs["modules"]:
        for register in module.hvi_registers:
            log.info(
                f"...Adding register: {register}, "
                f"initial value: 0 to module: {module.name}"
            )
            registers = scopes[module.name].registers
            hviRegister = registers.add(register, kthvi.RegisterSize.SHORT)
            hviRegister.initial_value = 0
    log.info("Finished Defining System")
    return


def start():
    global hvi_handle
    log.info("Compiling HVI...")
    hvi_handle = sequencer.compile()
    log.info("Loading HVI to HW...")
    hvi_handle.load_to_hw()
    log.info("Starting HVI...")
    hvi_handle.run(hvi_handle.no_wait)
    return


def close():
    log.info("Releasing HVI...")
    hvi_handle.release_hw()


def show_sequencer():
    return sequencer.sync_sequence.to_string(kthvi.OutputFormat.DEBUG)


# Helper Functions


def _get_module(name):
    return [i for i in modules if i.name == name][0]


def _get_current_sequence(module_name):
    return _get_module(module_name)._current_sequence[-1]


def _push_current_sequence(module_name, sequence):
    _get_module(module_name)._current_sequence.append(sequence)


def _pop_current_sequence(module_name):
    _get_module(module_name)._current_sequence.pop()


def _statement_name(sequence, name):
    statement_names = [s.name for s in sequence.statements if s.name.startswith(name)]
    if len(statement_names) == 0:
        statement_name = name
    else:
        statement_name = f"{name}_{len(statement_names)}"
    return statement_name


def _sync_statement_name(sequence, name):
    statement_names = [
        s.name for s in sequence.sync_statements if s.name.startswith(name)
    ]
    if len(statement_names) == 0:
        statement_name = name
    else:
        statement_name = f"{name}_{len(statement_names)}"
    return statement_name


# Setup resources Statements


def setup_triggers(
    module_name: str,
    triggers: List[str],
    direction: str = None,
    polarity: str = None,
    sync: str = None,
    hw_delay: int = None,
    mode: int = None,
):
    """Parameters (None means hardware is not changed for that parameter):
    direction: "INPUT" or "OUTPUT".
    polarity: "ACTIVE_HIGH" or "ACTIVE_LOW".
    sync: "SYNCH' or "IMMEDIATE".
    hw_delay (int): delay in ns before the output changes state.
    mode (int): 0 = LEVEL MODE, anything else = PULSE MODE with pulses width
                equal to the value in ns.
    """
    for trigger in triggers:
        if direction is None:
            pass
        elif direction.upper() == "OUTPUT":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.direction = kthvi.Direction.OUTPUT
        elif direction.upper() == "INPUT":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.direction = kthvi.Direction.INPUT
        else:
            raise ValueError(
                "If specified, trigger direction should be 'INPUT' or 'OUTPUT'"
            )

        if polarity is None:
            pass
        elif polarity.upper() == "ACTIVE_HIGH":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.polarity = kthvi.Polarity.ACTIVE_HIGH
        elif polarity.upper() == "ACTIVE_LOW":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.polarity = kthvi.Polarity.ACTIVE_LOW
        else:
            raise ValueError(
                "If specified, trigger polarity should be 'ACTIVE_HIGH' or 'ACTIVE_LOW'"
            )

        if sync is None:
            pass
        elif sync.upper() == "SYNC":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.sync_mode = kthvi.SyncMode.SYNC
        elif sync.upper() == "IMMEDIATE":
            system_definition.engines[module_name].triggers[
                trigger
            ].config.sync_mode = kthvi.SyncMode.IMMEDIATE
        else:
            raise ValueError(
                "If specified, trigger sync should be 'SYNC' or 'IMMEDIATE'"
            )

        if hw_delay is None:
            pass
        else:
            system_definition.engines[module_name].triggers[
                trigger
            ].config.hw_routing_delay = hw_delay

        if mode is None:
            pass
        elif mode == 0:
            system_definition.engines[module_name].triggers[
                trigger
            ].config.trigger_mode = kthvi.TriggerMode.LEVEL
        else:
            system_definition.engines[module_name].triggers[
                trigger
            ].config.trigger_mode = kthvi.TriggerMode.PULSE
            system_definition.engines[module_name].triggers[
                trigger
            ].config.pulse_length = mode


# Syncronous Block Statements


def start_syncWhile_register(name, engine, register, comparison, value, delay=70):
    global current_sync_sequence
    sequence = current_sync_sequence[-1]
    statement_name = _sync_statement_name(sequence, name)
    whileRegister = sequencer.sync_sequence.scopes[engine].registers[register]
    comparison_operator = getattr(kthvi.ComparisonOperator, comparison)

    log.info(f"Creating Synchronized While loop, {value} iterations...")
    condition = kthvi.Condition.register_comparison(
        whileRegister, comparison_operator, value
    )
    while_sequence = sequence.add_sync_while(statement_name, delay, condition)
    current_sync_sequence.append(while_sequence.sync_sequence)
    return


def end_syncWhile():
    global current_sync_sequence
    current_sync_sequence.pop()
    return


def start_sync_multi_sequence_block(name, delay=30):
    global current_block, modules
    sequence = current_sync_sequence[-1]
    statement_name = _sync_statement_name(sequence, name)
    block = sequence.add_sync_multi_sequence_block(statement_name, delay)
    current_block.append(block)
    for module in modules:
        module._current_sequence.append(block.sequences[module.name])
    return


def end_sync_multi_sequence_block():
    global current_block
    current_block.pop()
    for module in modules:
        module._current_sequence.pop()


# Native HVI Sequence Instructions


def if_register_comparison(name, module, register, comparison, value, delay=10):
    """
    Inserts an 'if' statement in the flow following instructions
    are only executed if condition evalutes to True. This should be terminated
    with 'end_if()' statement.
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    comparison_operator = getattr(kthvi.ComparisonOperator, comparison)
    if_condition = kthvi.Condition.register_comparison(
        register, comparison_operator, value
    )
    enable_matching_branches = True
    if_statement = sequence.add_if(
        statement_name, delay, if_condition, enable_matching_branches
    )
    _push_current_sequence(module, if_statement.if_branch.sequence)


def end_if(module):
    _pop_current_sequence(module)


def set_register(name, module, register, value, delay=10):
    """Sets <register> in <module> to <value>"""
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.scope.registers[register]
    log.info(f"......{statement_name}")
    instruction = sequence.add_instruction(
        statement_name, delay, sequence.instruction_set.assign.id
    )
    instruction.set_parameter(
        sequence.instruction_set.assign.destination.id, register_id
    )
    instruction.set_parameter(sequence.instruction_set.assign.source.id, value)


def read_register_runtime(module, register):
    register_runtime = hvi_handle.sync_sequence.scopes[module].registers[register]
    value = register_runtime.read()
    return value


def write_register_runtime(module, register, value):
    register_runtime = hvi_handle.sync_sequence.scopes[module].registers[register]
    register_runtime.write(value)
    return value


def incrementRegister(name, module, register, delay=10):
    """Increments <register> in <module>"""
    addToRegister(name, module, register, 1, delay)


def addToRegister(name, module, register, value, delay=10):
    """Adds <value> to <register> in <module>"""
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.scope.registers[register]
    log.info(f"......{statement_name}")
    instruction = sequence.add_instruction(
        statement_name, delay, sequence.instruction_set.add.id
    )
    instruction.set_parameter(sequence.instruction_set.add.destination.id, register_id)
    instruction.set_parameter(sequence.instruction_set.add.left_operand.id, register_id)
    instruction.set_parameter(sequence.instruction_set.add.right_operand.id, value)


def writeFpgaMemRegister(name: str, module, bank: str, offset: int, value, delay=10):
    """
    Writes <value> to module's FPGA register: <offset>, in <bank>.

    name : title given to this instruction.
    bank : name of the FPGA register bank.
    offset: Offset of register in bank lword addressed
    value : to be written to the register
            if str, the hvi register of that name is used to supply the value
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    bank_id = sequence.engine.fpga_sandboxes[0].fpga_memory_maps[bank]
    log.info(f"......{statement_name}")
    cmd = sequence.instruction_set.fpga_array_write
    instruction = sequence.add_instruction(statement_name, delay, cmd.id)
    instruction.set_parameter(cmd.fpga_memory_map.id, bank_id)
    instruction.set_parameter(cmd.fpga_memory_map_offset.id, offset)
    if type(value) is str:
        value = sequence.scope.registers[value]
    instruction.set_parameter(cmd.value.id, value)
    return


def readFpgaMemRegister(name: str, module, bank: str, offset: int, hvi_register: str, delay=10):
    """
    Reads from module's FPGA register, <register> into HVI register <hvi_register.

    name : title given to this instruction.
    bank : name of the FPGA register bank.
    offset: Offset of register in bank lword addressed
    hvi_register : name of hvi register to be read from the FPGA register
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    bank_id = sequence.engine.fpga_sandboxes[0].fpga_memory_maps[bank]
    log.info(f"......{statement_name}")
    cmd = sequence.instruction_set.fpga_array_read
    instruction = sequence.add_instruction(statement_name, delay, cmd.id)
    instruction.set_parameter(cmd.fpga_memory_map.id, bank_id)
    instruction.set_parameter(cmd.fpga_memory_map_offset.id, offset)
    dest_register = sequence.scope.registers[hvi_register]
    instruction.set_parameter(cmd.destination.id, dest_register)
    return


def writeFpgaRegister(name, module, register, value, delay=10):
    """
    Writes <value> to module's FPGA register: <register>.

    name : title given to this instruction.
    register : name of the FPGA register
    value : to be written to the register
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[register]
    log.info(f"......{statement_name}")
    reg_cmd = sequence.instruction_set.fpga_register_write
    instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
    instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
    if type(value) is str:
        value = sequence.scope.registers[value]
    instruction.set_parameter(reg_cmd.value.id, value)
    return


def readFpgaRegister(name, module, fpga_register, hvi_register, delay=10):
    """
    Reads from module's FPGA register: <register> into <hvi_register>.

    name : title given to this instruction.
    register : name of the FPGA register
    hvi_register : name of hvi register to be read from the FPGA register
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    register_id = sequence.engine.fpga_sandboxes[0].fpga_registers[fpga_register]
    log.info(f"......{statement_name}")
    reg_cmd = sequence.instruction_set.fpga_register_read
    instruction = sequence.add_instruction(statement_name, delay, reg_cmd.id)
    instruction.set_parameter(reg_cmd.fpga_register.id, register_id)
    dest_register = sequence.scope.registers[hvi_register]
    instruction.set_parameter(reg_cmd.destination.id, dest_register)
    return


def execute_actions(name, module, actions, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to execute all <actions>
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.info(f"......{statement_name}")
    actionCmd = sequence.instruction_set.action_execute
    actionParams = [sequence.engine.actions[action] for action in actions]
    instruction = sequence.add_instruction(statement_name, delay, actionCmd.id)
    instruction.set_parameter(actionCmd.action.id, actionParams)


def assert_triggers(name, module, triggers, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to assert all <triggers>
    triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.info(f"......{statement_name}")
    triggerCmd = sequence.instruction_set.trigger_write
    triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
    instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
    instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
    instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
    instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.ON)


def disassert_triggers(name, module, triggers, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to disassert all <triggers>
    triggers can be pxi0..pxi7 (but only if not committed to HVI system), smb1..smb8
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.info(f"......{statement_name}")
    triggerCmd = sequence.instruction_set.trigger_write
    triggerParams = [sequence.engine.triggers[trigger] for trigger in triggers]
    instruction = sequence.add_instruction(statement_name, delay, triggerCmd.id)
    instruction.set_parameter(triggerCmd.trigger.id, triggerParams)
    instruction.set_parameter(triggerCmd.sync_mode.id, kthvi.SyncMode.IMMEDIATE)
    instruction.set_parameter(triggerCmd.value.id, kthvi.TriggerValue.OFF)


def delay(name, module, delay=10):
    """
    Adds an instruction called <name> to sequence for <module> to the current block
    to delay for <delay> ns.
    """
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.info(f"......{statement_name}")
    sequence.add_delay(statement_name, delay)


# AWG specific HVI Sequence Instructions


def awg_set_amplitude(name, module, channel, value, delay=10):
    """
    Adds an instruction called <name> to <module>'s sequence to set amplitude
    of <channel> to <value>
    """
    module_name = module
    sequence = _get_current_sequence(module)
    statement_name = _statement_name(sequence, name)
    log.info(f"......{name}")
    for module in modules:
        if module.name == module_name:
            break
    command = module.handle.hvi.instruction_set.set_amplitude
    instruction = sequence.add_instruction(statement_name, delay, command.id)
    instruction.set_parameter(command.channel.id, channel)
    instruction.set_parameter(command.value.id, value)
