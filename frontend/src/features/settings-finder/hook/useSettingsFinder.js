import { useRef, useState } from "react";
import { useIsMutating, useQuery } from "@tanstack/react-query";

import { SETTINGS_API } from "../constants/query-keys";

const useSettingsFinder = ({ mode }) => {
  const markRef = useRef(null);
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const { data: processImageData } = useQuery({
    queryKey: [SETTINGS_API.queries, mode],
  });

  const isMutating = useIsMutating({
    mutationKey: [SETTINGS_API.mutations, mode],
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
