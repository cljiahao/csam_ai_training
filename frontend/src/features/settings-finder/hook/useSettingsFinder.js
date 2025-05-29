import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { SETTINGS_API } from "../constants/query-keys";

const useSettingsFinder = ({ mode }) => {
  const markRef = useRef(null);
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const { data: processImageData } = useQuery({
    queryKey: [SETTINGS_API.queries, mode],
  });

  return {
    state: {
      markRef,
      image,
      error,
      coordinates: processImageData?.coordinates,
    },
    action: { setImage, setError },
  };
};

export default useSettingsFinder;
