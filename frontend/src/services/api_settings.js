import { createFileRequestOptions, sendRequest } from ".";

export const uploadImage = async (mode, item, targetCount, formData) => {
  const url = `/api/settings/${mode}?item=${item}&target_count=${targetCount}`;
  const options = createFileRequestOptions("POST", formData);
  return await sendRequest(url, options);
};
