import {
  cloneElement,
  forwardRef,
  isValidElement,
  useImperativeHandle,
} from "react";
import useMarkCanvas from "./hooks/useMarkCanvas";

const MarkCanvas = forwardRef(({ children, imageSize }, ref) => {
  const markCanvasState = useMarkCanvas();
  const {
    state: { marks },
    action: { resetMarks, addMark, handleMark },
  } = markCanvasState;

  useImperativeHandle(ref, () => ({ resetMarks, addMark }));

  return (
    <svg
      className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
      width={imageSize?.width}
      height={imageSize?.height}
    >
      {children && isValidElement(children)
        ? cloneElement(children, {
            marks,
            imageSize,
            handleMark,
          })
        : null}
    </svg>
  );
});
MarkCanvas.displayName = "MarkCanvas";

export default MarkCanvas;
