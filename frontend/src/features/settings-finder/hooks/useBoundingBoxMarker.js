import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { MARKERS } from "@/core/constants";

const useBoundingBoxMarker = (mode, marks, imageSize) => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedSettings", mode],
  });

  const generateRectangles = useMemo(() => {
    if (!imageSize || !processImageData) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.fileName, mark);
    });

    return (processImageData.coordinates || []).map((file, index) => {
      const dx =
        Math.round(
          (file.norm_x_center - file.norm_batch_width / 2) *
            imageSize.width *
            100,
        ) / 100;
      const dy =
        Math.round(
          (file.norm_y_center - file.norm_batch_height / 2) *
            imageSize.height *
            100,
        ) / 100;
      const d_width =
        Math.round(file.norm_batch_width * imageSize.width * 100) / 100;
      const d_height =
        Math.round(file.norm_batch_height * imageSize.height * 100) / 100;

      return {
        id: index,
        x_start: dx,
        y_start: dy,
        width: d_width,
        height: d_height,
        r: MARKERS.temp.radius,
        color: MARKERS.static.color,
      };
    });
  }, [processImageData, marks, imageSize]);

  return { state: { generateRectangles } };
};

export default useBoundingBoxMarker;
