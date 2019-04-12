from enum import Enum


class LampyStatus(Enum):
    # Empty Node
    Empty = 0

    # Const node
    Const = 1

    # Output nodes
    Output_Undefined = 10
    Output_Empty = 11
    Output_Running = 12
    Output_Loading = 13
    Output_Done = 14

    # Input nodes
    Input_Empty = 21
    Input_Loading = 22
    Input_Done = 23


CONST_NODE = [LampyStatus.Const]
INPUT_NODE = [LampyStatus.Input_Empty, LampyStatus.Input_Loading, LampyStatus.Input_Done]
OUTPUT_NODE = [LampyStatus.Output_Undefined,LampyStatus.Output_Empty,LampyStatus.Output_Loading,
               LampyStatus.Output_Running,LampyStatus.Output_Done]
DONE_NODE = [LampyStatus.Output_Done, LampyStatus.Input_Done, LampyStatus.Const]