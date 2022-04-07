import request from "@/utils/request";

// 查询埋点列表
export function comparePublish(pk1, pk2) {
  return request({
    url: "/ios/publish/compare/" + pk1 + "/" + pk2 + "/",
    method: "get",
  });
}

// 查询埋点列表
export function listPublish(query) {
  return request({
    url: "/ios/publish/",
    method: "get",
    params: query
  });
}


// 查询版本列表
export function listBuildNo(query) {
  return request({
    url: "/ios/publish/builds/",
    method: "get",
    params: query
  });
}

// 通过json文件添加发布记录数据
export function addPublishByFile(query) {
  return request({
    url: "/ios/publish/byJson/",
    method: "post",
    params: query
  });
}
