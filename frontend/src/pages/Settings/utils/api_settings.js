import { API } from "../../../core/config";

export const getRange = async (name) => {
  const resp = await fetch(`${API}/Settings/get_range`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: name }),
  });
  return resp;
};

export const saveParameters = async (name, range) => {
  const resp = await fetch(`${API}/Settings/save_parameters`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: name, range: range }),
  });
  return resp;
};
