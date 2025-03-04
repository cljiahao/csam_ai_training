import useBoundingBoxMarker from "../hooks/useBoundingBoxMarker";

const BoundingBoxCanvas = ({ mode, marks, imageSize }) => {
  const {
    state: { generateRectangles },
  } = useBoundingBoxMarker(mode, marks, imageSize);

  return (
    <>
      {generateRectangles.map((rectangle) => {
        return (
          <rect
            key={rectangle.id}
            id={rectangle.id}
            x={rectangle.x_start}
            y={rectangle.y_start}
            width={rectangle.width}
            height={rectangle.height}
            rx={rectangle.r}
            ry={rectangle.r}
            stroke={rectangle.color}
            strokeWidth="2"
            fill="none"
          />
        );
      })}
    </>
  );
};

export default BoundingBoxCanvas;
