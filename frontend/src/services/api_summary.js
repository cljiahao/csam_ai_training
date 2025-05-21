import { createRequestOptions, sendRequest } from ".";

export const getSummaryData = async (method) => {
  const url = `/api/data_summary/${method.toLowerCase()}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
