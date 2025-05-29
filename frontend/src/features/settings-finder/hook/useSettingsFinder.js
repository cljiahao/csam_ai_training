import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";

const useSettingsFinder = ({ mode }) => {
  const markRef = useRef(null);
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const { data: processImageData } = useQuery({
    queryKey: ["processedSettings", mode],
  });
  const coordinates = processImageData?.coordinates;

  return {
    state: { markRef, image, error, coordinates },
    action: { setImage, setError },
  };
};

export default useSettingsFinder;
