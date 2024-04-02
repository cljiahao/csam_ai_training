import { API } from "../../../core/config";

const zipModel = async (modelName) => {
  const response = await fetch(`${API}/CMT/zip_model/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model_name: modelName }),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }
  const blob = await response.blob();
  return blob;
};

export default zipModel;
