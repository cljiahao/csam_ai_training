import { createRequestOptions, sendRequest } from ".";

export const getSummaryData = async () => {
  const url = "/api/data_summary/";
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
