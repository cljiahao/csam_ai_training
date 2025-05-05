import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { MARKERS } from "@/core/constants";

const useDotMarker = (mode, marks, imageSize) => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedSettings", mode],
  });

  const generateCircles = useMemo(() => {
    if (!imageSize || !processImageData) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.fileName, mark);
    });

    return (processImageData.coordinates || []).map((file, index) => {
      const dx = Math.round(file.norm_x_center * imageSize.width * 100) / 100;
      const dy = Math.round(file.norm_y_center * imageSize.height * 100) / 100;

      return {
        id: index,
        cx: dx,
        cy: dy,
        r: MARKERS.temp.radius,
        color: MARKERS.static.color,
      };
    });
  }, [processImageData, marks, imageSize]);

  return { state: { generateCircles } };
};

export default useDotMarker;
