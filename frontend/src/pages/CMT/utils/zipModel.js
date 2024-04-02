import { API } from "../../../core/config";

const zipModel = async (modelName) => {
  try {
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
  } catch (error) {
    console.error("Failed to zip model:", error);
    throw error;
  }
};

export default zipModel;
