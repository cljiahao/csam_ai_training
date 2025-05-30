import { useEffect } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const useUtilityPanel = ({ method }) => {
  const [isChecked, setChecked] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    if (!method || method != "retrain") {
      setChecked(false);
      navigate(`/CDS?method=train`);
    } else {
      setChecked(true);
    }
  }, [method, navigate]);

  const onCheckChange = (checkState) => {
    if (checkState) navigate(`/CDS?method=retrain`);
    else navigate(`/CDS?method=train`);
    setChecked(checkState);
  };

  return { state: { isChecked }, action: { onCheckChange } };
};

export default useUtilityPanel;
