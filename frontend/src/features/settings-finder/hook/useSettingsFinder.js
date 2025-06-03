import { useRef, useState } from "react";
import { useIsMutating } from "@tanstack/react-query";
import { MUTATION_KEYS } from "@/constants/api-keys";
import { useQueryImageData } from "../api/settings-finder";

const useSettingsFinder = ({ mode }) => {
  const markRef = useRef(null);
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const imageData = useQueryImageData(mode);

  const isMutating = useIsMutating({
    mutationKey: [MUTATION_KEYS.API_SETTINGS, mode],
  });

  return {
    state: {
      coordinates: imageData?.coordinates,
      error,
      image,
      isLoading: isMutating > 0,
      markRef,
    },
    action: { setImage, setError },
  };
};

export default useSettingsFinder;
