import Loading from "@/components/static/loading";
import Error from "@/components/static/error";
import ImageHolder from "@/components/widgets/image-holder/ImageHolder";
import MarkCanvas from "@/components/widgets/mark-canvas/MarkCanvas";
import SettingsFinderContext from "./context/SettingsFinderContext";
import useSettingsFinder from "./hook/useSettingsFinder";
import UploadForm from "./subfeatures/upload-form/UploadForm";
import { MODE_PARAMS } from "@/constants/url-params";

const SettingsFinder = ({ mode }) => {
  const {
    state: { markRef, image, error, coordinates, isLoading },
    action: { setImage, setError },
  } = useSettingsFinder({ mode });

  const canvasType = mode.toLowerCase() === MODE_PARAMS.BATCH ? "rect" : "dot";

  return (
    <SettingsFinderContext.Provider value={{ setImage, setError }}>
      <div className="h-full">
        <ImageHolder className="h-5/6" image={image} placeholder_text={mode}>
          {error ? (
            <Error message={error} />
          ) : isLoading ? (
            <Loading />
          ) : (
            <MarkCanvas
              ref={markRef}
              canvasType={canvasType}
              coordinates={coordinates}
              showStatic
            />
          )}
        </ImageHolder>
        <div className="h-1/6">
          <UploadForm mode={mode} />
        </div>
      </div>
    </SettingsFinderContext.Provider>
  );
};

export default SettingsFinder;
