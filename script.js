import http from 'k6/http';
import {htmlReport} from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

/*
 * This is the main script for the K6 load testing tool
 * ====================================================
 *
 * Execute this command to run the script:
 *
 *      k6 run --vus 10 --duration 20s \
 *              -e MIDDLEWARE_HOST=localhost:8000 \
 *              -e SERVING_TYPE=tfserving|torchserve|triton_tensorflow|triton_pytorch \
 *              script.js
 *
 * The output metrics are documented here: https://k6.io/docs/using-k6/metrics/#http-specific-built-in-metrics
 *
*/

// noinspection JSUnusedGlobalSymbols
export function handleSummary(data) {
    return {[`${Date.now()}-k6-report-${__ENV.SERVING_TYPE}.html`]: htmlReport(data)}

}

// noinspection JSUnusedGlobalSymbols
export default function () {
    http.get(`http://${__ENV.MIDDLEWARE_HOST}/randinfer/${__ENV.SERVING_TYPE}`);
}
