import { DataTable } from "@/components/widgets/data-table/DataTable";
import { METHOD_PARAMS } from "@/constants/url-params";
import {
  BaseColumnCells,
  EvalColumnCells,
  InfoColumnCells,
  ReTrainButtonColumn,
  ReTrainColumnCells,
  TrainButtonColumn,
} from "./components/ColumnCells";
import useSummaryTable from "./hooks/useSummaryTable";

const SummaryTable = ({ method }) => {
  const {
    state: { dataTable },
    action: { navigate },
  } = useSummaryTable(method);

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
        columns={method === METHOD_PARAMS.TRAIN ? trainColumns : reTrainColumns}
        data={dataTable?.train_sets_list ?? []}
      />
    </div>
  );
};

export default SummaryTable;
