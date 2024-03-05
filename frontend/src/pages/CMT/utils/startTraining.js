import { API } from "../../../core/config";

const startTraining = async (parameters) => {
  console.log(parameters);
  const resp = await fetch(`${API}/CMT/train_model`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(parameters),
  });
  const json = await resp.json();
  return json;
};

export default startTraining;
