import { cn } from "@/lib/utils";
import {
  cloneElement,
  forwardRef,
  isValidElement,
  useImperativeHandle,
} from "react";
import { useIsMutating } from "@tanstack/react-query";

import Error from "@/components/static/error";
import PanAndZoom from "./components/PanAndZoom";
import Placeholder from "./components/PlaceHolder";
import ImageHolderContext from "./context/ImageHolderContext";
import { usePanZoom } from "./hooks/usePanZoom";
import useImageInfo from "./hooks/useImageInfo";
import Loading from "@/components/static/loading";

const ImageHolder = forwardRef(
  ({ className, children, image, error, placeholder_text, mode }, ref) => {
    const isMutating = useIsMutating({ mutationKey: ["imageProcess", mode] }); // For useMutation

    useImperativeHandle(ref, () => ({
      get moveActive() {
        return moveActive; // Always gets latest value
      },
      updateCoords,
      updateScale,
      resetCoords,
    }));

    const panZoomState = usePanZoom();
    const {
      state: { displayRef, moveActive },
      action: { updateCoords, updateScale, resetCoords },
    } = panZoomState;

    const imageState = useImageInfo();

    const {
      state: { imageSize },
    } = imageState;

    return (
      <ImageHolderContext.Provider value={{ image, panZoomState, imageState }}>
        <div
          className={cn("flex-center h-full w-full overflow-hidden", className)}
          ref={displayRef}
        >
          {error ? (
            <Error message={error} />
          ) : isMutating > 0 ? (
            <Loading />
          ) : (
            <>
              <Placeholder
                className={image ? "hidden" : ""}
                text={placeholder_text}
              />
              <PanAndZoom className={image ? "" : "hidden"}>
                {children && isValidElement(children)
                  ? cloneElement(children, {
                      imageSize,
                    })
                  : null}
              </PanAndZoom>
            </>
          )}
        </div>
      </ImageHolderContext.Provider>
    );
  },
);
ImageHolder.displayName = "ImageHolder";

export default ImageHolder;
