import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { METHOD_PARAMS } from "@/constants/url-params";

const useUtilityPanel = ({ method }) => {
  const [isChecked, setChecked] = useState(false);

  const navigate = useNavigate();
  const location = useLocation(); // use current path /CDS where summary-bar lives

  useEffect(() => {
    if (!method || method != METHOD_PARAMS.RETRAIN) {
      if (method != METHOD_PARAMS.TRAIN) {
        const params = new URLSearchParams({
          method: METHOD_PARAMS.TRAIN,
        });
        navigate(`${location.pathname}?${params}`);
        setChecked(false);
      }
    } else {
      setChecked(true);
    }
  }, [method, navigate, location]);

  const onCheckChange = (checkState) => {
    const params = new URLSearchParams({
      method: checkState ? METHOD_PARAMS.RETRAIN : METHOD_PARAMS.TRAIN,
    });
    navigate(`${location.pathname}?${params}`);
    setChecked(checkState);
  };

  return { state: { isChecked }, action: { onCheckChange } };
};

export default useUtilityPanel;
