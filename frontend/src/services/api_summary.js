import { createRequestOptions, sendRequest } from ".";

export const getSummaryData = async () => {
  const url = "/api/summary/eval_base_set_count";
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
