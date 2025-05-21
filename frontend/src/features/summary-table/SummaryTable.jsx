import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

import { DataTable } from "@/components/widgets/data-table/DataTable";
import { getSummaryData } from "@/services/api_summary";
import {
  BaseColumnCells,
  EvalColumnCells,
  InfoColumnCells,
  ReTrainButtonColumn,
  ReTrainColumnCells,
  TrainButtonColumn,
} from "./components/ColumnCells";

const SummaryTable = ({ method }) => {
  const { data: dataTable } = useQuery({
    queryKey: ["dataTable", method],
    queryFn: async () => await getSummaryData(method),
    enabled: true,
    staleTime: 0,
    refetchInterval: 10000,
  });

  const navigate = useNavigate();

  const trainColumns = [
    InfoColumnCells(),
    EvalColumnCells(),
    BaseColumnCells(),
    TrainButtonColumn(dataTable, navigate),
  ];

  const reTrainColumns = [
    InfoColumnCells(),
    EvalColumnCells(),
    ReTrainColumnCells(),
    ReTrainButtonColumn(dataTable, navigate),
  ];

  return (
    <div className="flex flex-1 overflow-auto p-4">
      <DataTable
        className="bg-white bg-opacity-80"
        columns={method === "train" ? trainColumns : reTrainColumns}
        data={dataTable?.train_sets_list ?? []}
      />
    </div>
  );
};

export default SummaryTable;
