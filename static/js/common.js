$(document).ready(function () {
    const radioMimeChecked = $("input[name='mime']:checked")[0];
    document.previousMime = radioMimeChecked.value;
    updateButtonState(radioMimeChecked);
    // 检测页面是否从缓存中恢复（即通过返回按钮返回）
    window.addEventListener('pageshow', function (event) {
        if (event.persisted)
            window.location.reload(); // 强制刷新页面
    });
})

/**
 * 更新按钮状态
 */
function updateButtonState(dom) {
    const buttonForm = document.getElementById("buttonForm");
    buttonForm.disabled = dom.value.trim().startsWith("application/json");
}

/**
 * 清屏按钮的响应函数
 */
function clearDiv(dom) {
    $(dom).text("");
}

/**
 * form格式参数转json
 */
function formToJson(formString) {
    let jsonObject = {};
    for (let keyValue of formString.split("&")) {
        let item = keyValue.split("=");
        jsonObject[decodeURI(item[0])] = decodeURI(item[1]);
    }
    return JSON.stringify(jsonObject);
}

/**
 * json格式参数转form
 */
function jsonToForm(jsonString) {
    let jsonObj = JSON.parse(jsonString);
    return Object.keys(jsonObj)
        .map(key => `${encodeURI(key)}=${encodeURI(jsonObj[key])}`)
        .join("&");
}

/**
 * 格式化输入数据
 */
function formatData(dom) {
    let mime = dom.value;
    let outputBox = $("#textParams");
    if ((document.previousMime.startsWith("application/x-www-form-urlencoded") || document.previousMime.startsWith("multipart/form-data")) && mime.startsWith("application/json"))
        outputBox.val(formToJson(outputBox.val()));
    if (document.previousMime.startsWith("application/json") && (mime.startsWith("application/x-www-form-urlencoded") || mime.startsWith("multipart/form-data")))
        outputBox.val(jsonToForm(outputBox.val()));
    document.previousMime = mime;
}

/**
 * 请求按钮的响应函数
 */
async function getCustom(dom, with_ajax) {
    let requestMethod = $("input[name='requestMethod']:checked").val().trim();
    let mime = $("input[name='mime']:checked").val().trim();
    let url = $("#inputUrl").val().trim();
    let data = $("#textParams").val().trim();
    let divOutput = $("#divOutput");
    let formUpload = $("#formUpload");
    let fileUpload = $("#fileUpload");

    if (with_ajax) {
        if (mime.startsWith("multipart/form-data")) {
            formUpload.attr("enctype", mime);
            let formData = new FormData(formUpload[0]);
            for (let keyValue of data.split("&")) {
                let item = keyValue.split("=");
                formData.append(item[0], item[1]);
            }
            data = formData;
        }
        let response = await fetch(url, {
            method: requestMethod,
            headers: mime.startsWith("multipart/form-data") ? {} : {"Content-Type": mime},
            body: data
        });
        if (response.ok) {
            let responseText = await response.text();
            divOutput.append("--------------------------------------------------");
            divOutput.append($("<div></div>").html("<strong><i>请求: </i></strong><pre>" + data + "</pre>"));
            divOutput.append($("<div></div>").html("<strong><i>响应: </i></strong><span>" + responseText + "</span>"));
        } else {
            let responseText = await response.text();
            divOutput.append("--------------------------------------------------");
            divOutput.append($("<div></div>").html("<strong><i>请求: </i></strong><pre>" + data + "</pre>"));
            divOutput.append($("<div></div>").html("<strong><i>响应: </i></strong><span class='spanErrors'>" + responseText + "</span>"));
        }
    } else {
        formUpload.attr("action", url);
        formUpload.attr("method", requestMethod);
        formUpload.attr("enctype", mime);
        try {
            for (let keyValue of data.split("&")) {
                let item = keyValue.split("=");
                let newInput = $("<input class='inputHiddenForm'/>").attr("type", "hidden").attr("name", item[0]).attr("value", item[1]);
                formUpload.append(newInput);
            }
            if (!fileUpload.val()) {
                fileUpload.prop("disabled", true);
            }
            formUpload.submit();
        } finally {
            $("input.inputHiddenForm").remove();
            fileUpload.prop("disabled", false);
        }
    }
}