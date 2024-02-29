import { API } from "../../../core/config";

const setTrackbar = async (range) => {
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

export default setTrackbar;
