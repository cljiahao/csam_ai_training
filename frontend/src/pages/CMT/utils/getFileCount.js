import { API } from "../../../core/config";

const getFileCount = async (item, folder) => {
  const resp = await fetch(`${API}/CMT/ds_file_count`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item, folder: folder }),
  });
  const json = await resp.json();
  return json;
};

export default getFileCount;
