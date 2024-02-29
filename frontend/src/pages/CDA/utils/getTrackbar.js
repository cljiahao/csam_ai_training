import { API } from "../../../core/config";

const getTrackbar = async () => {
  const resp = await fetch(`${API}/CDA/get_trackbar`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getTrackbar;
