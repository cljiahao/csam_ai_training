import { API } from "../../../core/config";

const startEvaluation = async (model, item) => {
  const resp = await fetch(`${API}/CMT/evaluate_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model: model, item: item }),
  });
  const json = await resp.json();
  return json;
};

export default startEvaluation;
