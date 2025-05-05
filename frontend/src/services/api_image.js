import { createRequestOptions, sendRequest } from ".";

export const getImageSrc = async (src_path) => {
  const url = `/api/csam_image/${src_path}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
