import { useRef, useState } from "react";
import { useIsMutating, useQuery } from "@tanstack/react-query";
import { MUTATION_KEYS, QUERY_KEYS } from "@/constants/api-keys";

const useSettingsFinder = ({ mode }) => {
  const markRef = useRef(null);
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const { data: processImageData } = useQuery({
    queryKey: [QUERY_KEYS.API_SETTINGS, mode],
  });

  const isMutating = useIsMutating({
    mutationKey: [MUTATION_KEYS.API_SETTINGS, mode],
  });

  return {
    state: {
      markRef,
      image,
      error,
      coordinates: processImageData?.coordinates,
      isLoading: isMutating > 0,
    },
    action: { setImage, setError },
  };
};

export default useSettingsFinder;
