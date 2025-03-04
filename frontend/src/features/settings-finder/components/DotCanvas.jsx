import useDotMarker from "../hooks/useDotMarker";

const DotCanvas = ({ mode, marks, imageSize }) => {
  const {
    state: { generateCircles },
  } = useDotMarker(mode, marks, imageSize);

  return (
    <>
      {generateCircles.map((circle) => {
        return (
          <circle
            key={circle.id}
            id={circle.id}
            cx={circle.cx}
            cy={circle.cy}
            r={circle.r}
            stroke={circle.color}
            strokeWidth="2"
            fillOpacity="0"
          />
        );
      })}
    </>
  );
};

export default DotCanvas;
