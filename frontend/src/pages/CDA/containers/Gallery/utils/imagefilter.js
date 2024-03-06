import cv from "@techstark/opencv-js";
import getImages from "../../../utils/getImage";

const imageFilter = async (random, range, image_hold, canvas_hold) => {
  try {
    if (cv.getBuildInformation) {
      for (const [i, src] of random.entries()) {
        const file_blob = await getImages(src);
        image_hold[i].current.src = URL.createObjectURL(file_blob);
        image_hold[i].current.onload = () => {
          const img = cv.imread(image_hold[i].current);
          const cx = img.size().width / 2;
          const cy = img.size().height / 2;

          // Split image, threshold for background only mask and return background as full white
          const channel = new cv.MatVector();
          cv.split(img, channel);
          let combine = new cv.Mat();
          for (let j = 0; j < channel.size() - 1; ++j) {
            const cn_thres = new cv.Mat();
            cv.threshold(channel.get(j), cn_thres, 100, 255, cv.THRESH_BINARY);
            if (j === 0) combine = cn_thres;
            cv.bitwise_and(combine, cn_thres, combine);
          }
          img.setTo(new cv.Scalar.all(255), combine);

          // Convert to grayscale
          const gray = new cv.Mat();
          cv.cvtColor(img, gray, cv.COLOR_RGBA2GRAY);

          // Threshold for chip contours
          const thres = new cv.Mat();
          cv.threshold(
            gray,
            thres,
            range.mask.Thresh,
            255,
            cv.THRESH_BINARY_INV,
          );

          // Erode to return single chip
          const e_ones = cv.Mat.ones(
            range.mask.Erode_y,
            range.mask.Erode_x,
            cv.CV_8U,
          );
          const erode = new cv.Mat();
          cv.erode(
            thres,
            erode,
            e_ones,
            new cv.Point(-1, -1),
            1,
            cv.BORDER_CONSTANT,
            cv.morphologyDefaultBorderValue(),
          );

          const contours = new cv.MatVector();
          const hierarchy = new cv.Mat();
          cv.findContours(
            erode,
            contours,
            hierarchy,
            cv.RETR_EXTERNAL,
            cv.CHAIN_APPROX_SIMPLE,
          );

          // Get largest chip which is also near the center of the image
          let area = 0;
          let maxc = 0;
          for (let k = 0; k < contours.size(); ++k) {
            let cnt = contours.get(k);
            let rect = cv.boundingRect(cnt);
            if (
              area < cv.contourArea(cnt) &&
              cx - rect.width / 2 <= rect.x + rect.width / 2 &&
              rect.x <= cx &&
              cy - rect.height / 2 <= rect.y + rect.height / 2 &&
              rect.y <= cy
            ) {
              area = cv.contourArea(cnt);
              maxc = k;
            }
          }

          // Draw the mask of the largest center image
          const color = new cv.Scalar.all(255);
          let blank = new cv.Mat(
            img.rows,
            img.cols,
            img.type(),
            [0, 0, 0, 255],
          );
          cv.drawContours(blank, contours, maxc, color, -1);
          const d_ones = cv.Mat.ones(3, 3, cv.CV_8U);
          cv.dilate(
            blank,
            blank,
            d_ones,
            new cv.Point(-1, -1),
            1,
            cv.BORDER_CONSTANT,
            cv.morphologyDefaultBorderValue(),
          );

          // Show defect only
          const single = new cv.Mat();
          cv.bitwise_and(img, blank, single);
          const hsv = new cv.Mat();
          cv.cvtColor(single, hsv, cv.COLOR_RGB2HSV_FULL);
          const col_arr = Object.values(range.hsv);
          let low = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [
            col_arr[0],
            col_arr[2],
            col_arr[4],
            0,
          ]);
          let high = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [
            col_arr[1],
            col_arr[3],
            col_arr[5],
            255,
          ]);
          const mask = new cv.Mat();
          cv.inRange(hsv, low, high, mask);
          const inverse = new cv.Mat();
          cv.bitwise_not(mask, inverse);
          img.setTo(new cv.Scalar(0, 0, 0, 255), inverse);

          cv.imshow(canvas_hold[i].current, img);
          img.delete();
          channel.delete();
          combine.delete();
          gray.delete();
          thres.delete();
          e_ones.delete();
          erode.delete();
          contours.delete();
          hierarchy.delete();
          blank.delete();
          d_ones.delete();
          single.delete();
          hsv.delete();
          low.delete();
          high.delete();
          mask.delete();
          inverse.delete();
        };
      }
    }
  } catch (e) {
    console.log(e);
  }
};

export default imageFilter;
