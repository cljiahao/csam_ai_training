import useBoundingBoxMarker from "../hooks/useBoundingBoxMarker";

const BoundingBoxCanvas = ({ imageSize, marks, coordinates }) => {
  const {
    state: { generateRectangles },
  } = useBoundingBoxMarker(imageSize, marks, coordinates);

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
