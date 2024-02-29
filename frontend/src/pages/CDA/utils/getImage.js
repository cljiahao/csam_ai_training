import { API } from "../../../core/config";

const getImages = async (src) => {
  const resp = await fetch(`${API}/CDA/get_image/${src}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const blob = await resp.blob();
  return blob;
};

export default getImages;
