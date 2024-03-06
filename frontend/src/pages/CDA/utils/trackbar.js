import { API } from "../../../core/config";

export const getTrackbar = async () => {
  const resp = await fetch(`${API}/CDA/get_trackbar`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export const setTrackbar = async (range) => {
  const resp = await fetch(`${API}/CDA/set_trackbar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(range),
  });
  const json = await resp.json();
  return json;
};
