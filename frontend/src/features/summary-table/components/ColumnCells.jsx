import { Button } from "@/components/ui/button";
import { LuArrowUpDown } from "react-icons/lu";

const toCommaNumbers = (value) => {
  return value.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
};

export const InfoColumnCells = () => {
  return {
    header: "Information",
    columns: [
      {
        accessorKey: "id",
        header: ({ column }) => {
          return (
            <Button
              className="text-sm underline"
              variant="ghost"
              onClick={() =>
                column.toggleSorting(column.getIsSorted() === "asc")
              }
            >
              S/N
              <LuArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
      },
      {
        accessorKey: "item",
        header: "Item Type",
      },
    ],
  };
};

export const EvalColumnCells = () => {
  return {
    header: "Evaluation Sets",
    columns: [
      {
        accessorKey: "eval_data.colors_count.total_sum",
        header: "Colors",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.eval_data.colors_count.total_sum);
        },
      },
      {
        accessorKey: "eval_data.thousands_count.total_sum",
        header: "Thousands",
        cell: ({ row }) => {
          return toCommaNumbers(
            row.original.eval_data.thousands_count.total_sum,
          );
        },
      },
      {
        accessorKey: "eval_data.mass_pro_count.total_sum",
        header: "Mass Prod",
        cell: ({ row }) => {
          return toCommaNumbers(
            row.original.eval_data.mass_pro_count.total_sum,
          );
        },
      },
    ],
  };
};

export const BaseColumnCells = () => {
  return {
    header: "Augment BaseSets",
    columns: [
      {
        accessorKey: "train_data.no_of_g",
        header: "G",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.train_data.no_of_g);
        },
      },
      {
        accessorKey: "train_data.no_of_ng",
        header: "NG",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.train_data.no_of_ng);
        },
      },
      {
        accessorKey: "train_data.no_of_others",
        header: "Others",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.train_data.no_of_others);
        },
      },
    ],
  };
};

export const ReTrainColumnCells = () => {
  return {
    header: "Re-Train Sets",
    columns: [
      {
        accessorKey: "train_data.no_of_g",
        header: "G",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.train_data.no_of_g);
        },
      },
      {
        accessorKey: "train_data.no_of_ng",
        header: "NG",
        cell: ({ row }) => {
          return toCommaNumbers(row.original.train_data.no_of_ng);
        },
      },
    ],
  };
};

export const TrainButtonColumn = (dataTable, navigate) => {
  return {
    accessorKey: "action",
    header: "Action",
    cell: ({ row }) => {
      const { item, eval_data, train_data } = row.original;

      const isEvalThresHoldMet =
        eval_data.colors_count.total_sum >= dataTable.colors_threshold &&
        eval_data.thousands_count.total_sum >= dataTable.thousands_threshold &&
        eval_data.mass_pro_count.total_sum >= dataTable.mass_pro_threshold;

      const isBaseThresHoldMet =
        2 * dataTable.augment_multiplier * train_data.no_of_ng -
          train_data.no_of_others <=
          train_data.no_of_g && train_data.no_of_ng != 0;

      const isConditionMet = isEvalThresHoldMet && isBaseThresHoldMet;

      const handleClick = () => {
        if (isConditionMet) {
          navigate(`/CMT?method=train&item=${item}`);
        }
      };

      return (
        <Button
          className={`${isConditionMet ? "bg-green-400 hover:bg-green-300" : "bg-red-300"}`}
          variant="outline"
          disabled={!isConditionMet}
          onClick={handleClick}
        >
          {isConditionMet ? "Train" : "Insufficient"}
        </Button>
      );
    },
  };
};

export const ReTrainButtonColumn = (dataTable, navigate) => {
  return {
    accessorKey: "action",
    header: "Action",
    cell: ({ row }) => {
      const { item, eval_data, train_data } = row.original;

      const isEvalThresHoldMet =
        eval_data.colors_count.total_sum >= dataTable.colors_threshold &&
        eval_data.thousands_count.total_sum >= dataTable.thousands_threshold &&
        eval_data.mass_pro_count.total_sum >= dataTable.mass_pro_threshold;

      const isReTrainThresHoldMet =
        train_data.no_of_g > 0 && train_data.no_of_ng > 0;

      const isConditionMet = isEvalThresHoldMet && isReTrainThresHoldMet;

      const handleClick = () => {
        if (isConditionMet) {
          navigate(`/CMT?method=retrain&item=${item}`);
        }
      };

      return (
        <Button
          className={`${isConditionMet ? "bg-green-400 hover:bg-green-300" : "bg-red-300"}`}
          variant="outline"
          disabled={!isConditionMet}
          onClick={handleClick}
        >
          {isConditionMet ? "Re-Train" : "Insufficient"}
        </Button>
      );
    },
  };
};
