import { API } from "../core/config";

const process = async (range) => {
  const resp = await fetch(`${API}/CDA/process_img`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(range),
  });
  const json = await resp.json();
  return json;
};

export default process;
