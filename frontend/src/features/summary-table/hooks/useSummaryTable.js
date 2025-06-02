import { useNavigate } from "react-router-dom";

import { useQueryDataTable } from "../api/summary-table";

const useSummaryTable = (mode) => {
  const dataTable = useQueryDataTable(mode);

  const navigate = useNavigate();
  return { state: { dataTable }, action: { navigate } };
};

export default useSummaryTable;
