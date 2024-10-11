import widgets from "@jupyter-widgets/base";
import data from "../package.json";

export class ClearTextModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: 'ClearTextModel',
            _model_module: data.name,
            _model_module_version: data.version,

            _view_name: 'ClearTextView',
            _view_module: data.name,
            _view_module_version: data.version,

            value: '',
            disabled: false,
            placeholder: '',
            continuous_update: false,
            style: null
        }
    }
}

export class UploadView extends widgets.DOMWidgetView {
    render() {
        super.render();
        console.log('---- RENDERED! ----');
    }
}
