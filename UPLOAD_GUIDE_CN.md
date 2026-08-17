# MS-TES v10.1.0 更新步骤

## 推荐方案

保留旧 tag、旧 release 和旧 DOI 版本，不覆盖历史文件。将当前代码作为新版本 `v10.1.0` 发布。

GitHub 仓库使用两个轻量源码包。约 341 MB 的上游生成结果不进入 Git 历史，因为它们可以由源码包中的注册输入和代码完整重建。

## GitHub 主分支

目标仓库：`https://github.com/ChunleiWu-tech/MS-TES`

1. 打开仓库的 `main` 分支。
2. 更新根目录 `README.md`。
3. 上传 `CITATION.cff`、`RELEASE_NOTES.md`、`.gitignore`、`requirements.txt`、`requirements-lock.txt`、两个源码 ZIP 和 `SHA256SUMS.txt`。
4. 建议提交信息：`Release v10.1.0 reproducible source packages`。
5. 旧的 V171 ZIP 暂不删除。确认新 release 和 DOI 版本正常后，再决定是否从当前分支移除；历史 commit 仍会保留旧文件。

## GitHub Release

1. 进入仓库右侧 `Releases`。
2. 选择 `Draft a new release`。
3. 新建 tag：`v10.1.0`，目标分支选择 `main`。
4. Release title：`MS-TES v10.1.0: evidence-bounded molten-salt screening`。
5. Release notes 可直接使用 `RELEASE_NOTES.md`。
6. 附加两个源码 ZIP 和 `SHA256SUMS.txt`。
7. 设为 Latest release 后发布。

## DOI

如果 Zenodo 已与该 GitHub 仓库连接，新建 GitHub Release 通常会生成一个新的 Zenodo 版本。若没有自动生成，则在原 Zenodo 记录中选择 `New version`，导入旧版本文件，再用本次文件替换代码资产并发布。

- 旧版本 DOI 不会被覆盖。
- 新版本会获得新的 version DOI。
- Concept DOI 保持不变，并解析到最新版本。
- 如果稿件引用的是 Concept DOI，可以继续使用原 DOI。
- 如果稿件引用的是旧版 version DOI，为确保读者获得本次代码，应改为新版本 DOI。

仅更新 GitHub 的 `main` 分支不会改变已发表 DOI 对应的归档文件。要让 DOI 页面包含新代码，必须创建新的 Zenodo 版本或由新的 GitHub Release 触发版本归档。

