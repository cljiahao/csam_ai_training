import { useMemo } from "react";

import { MARKERS } from "@/core/constants";

const useDotMarker = (imageSize, coordinates, marks) => {
  const generateCircles = useMemo(() => {
    if (!imageSize || !coordinates) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.fileName, mark);
    });

    return (coordinates || []).map((file, index) => {
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
  }, [coordinates, marks, imageSize]);

  return { state: { generateCircles } };
};

export default useDotMarker;
