import { ArrowUpDown } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

import { DataTable } from "@/components/widgets/data-table/DataTable";
import { Button } from "@/components/ui/button";
import { getSummaryData } from "@/services/api_summary";

const SummaryTable = () => {
  const { data: dataTable } = useQuery({
    queryKey: ["dataTable"],
    queryFn: async () => await getSummaryData(),
    enabled: true,
    refetchInterval: 5000,
  });

  const navigate = useNavigate();

  const toCommaNumbers = (value) => {
    return value.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
  };

  const columns = [
    {
      header: "Info",
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
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            );
          },
        },
        {
          accessorKey: "item",
          header: "Item Type",
        },
      ],
    },
    {
      header: "Eval",
      columns: [
        {
          accessorKey: "eval_data.colors_count.total_sum",
          header: "Colors",
          cell: ({ row }) => {
            return toCommaNumbers(
              row.original.eval_data.colors_count.total_sum,
            );
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
    },
    {
      header: "Base",
      columns: [
        {
          accessorKey: "base_data.no_of_g",
          header: "G",
          cell: ({ row }) => {
            return toCommaNumbers(row.original.base_data.no_of_g);
          },
        },
        {
          accessorKey: "base_data.no_of_ng",
          header: "NG",
          cell: ({ row }) => {
            return toCommaNumbers(row.original.base_data.no_of_ng);
          },
        },
        {
          accessorKey: "base_data.no_of_others",
          header: "Others",
          cell: ({ row }) => {
            return toCommaNumbers(row.original.base_data.no_of_others);
          },
        },
      ],
    },
    {
      accessorKey: "action",
      header: "Action",
      cell: ({ row }) => {
        const { item, eval_data, base_data } = row.original;

        const isEvalThresHoldMet =
          eval_data.colors_count.total_sum >= dataTable.colors_threshold &&
          eval_data.thousands_count.total_sum >=
            dataTable.thousands_threshold &&
          eval_data.mass_pro_count.total_sum >= dataTable.mass_pro_threshold;

        const isBaseThresHoldMet =
          2 * dataTable.augment_multiplier * base_data.no_of_ng -
            base_data.no_of_others <=
          base_data.no_of_g;

        const handleClick = () => {
          if (isEvalThresHoldMet && isBaseThresHoldMet) {
            navigate(`/CMT?method=train&item=${item}`);
          }
        };

        return (
          <Button
            className={`${isEvalThresHoldMet && isBaseThresHoldMet ? "bg-green-400 hover:bg-green-300" : "bg-red-300"}`}
            variant="outline"
            disabled={!isEvalThresHoldMet || !isBaseThresHoldMet}
            onClick={handleClick}
          >
            {isEvalThresHoldMet && isBaseThresHoldMet
              ? "Train"
              : "Insufficient"}
          </Button>
        );
      },
    },
  ];

  return (
    <div className="flex flex-1 overflow-auto p-4">
      <DataTable
        className="bg-white bg-opacity-80"
        columns={columns}
        data={dataTable?.eval_base_sets ?? []}
      />
    </div>
  );
};

export default SummaryTable;
