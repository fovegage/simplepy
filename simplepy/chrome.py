import json
import os
import zipfile

manifest_json = {
    "manifest_version": 2,
    "name": "Inject",
    "version": "1.0.0",
    "description": "Inject Plugin",
    "content_scripts": [
        {
            "matches": ["<all_urls>"],
            "js": ["content.js"],
            "run_at": "document_end"
        }
    ],
    "background": {
        "scripts": [
            "background.js"
        ],
        "persistent": True
    },
    "permissions": [
        "storage",
        "unlimitedStorage",
        "cookies",
        "notifications",
        "clipboardRead",
        "clipboardWrite",
        "webRequest",
        "webRequestBlocking",
        "*://*/*"
    ],
    # "content_security_policy": "script-src 'self' 'unsafe-eval'; object-src 'self'",
    "externally_connectable": {
        "matches": ["<all_urls>"]
    }
}
background_js = open(r'E:\code\codeline\libs\resources\js\filter.js').read()

content_js = open(r'E:\code\codeline\libs\resources\js\content.js', encoding='utf-8').read()


def gen_plugin():
    base_path = os.path.dirname(__file__)
    plugin_path = os.path.join(base_path, f'resources/plugins/inject_plugin.zip')

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", json.dumps(manifest_json, ensure_ascii=False, indent=4))
        zp.writestr("background.js", background_js)
        zp.writestr('content.js', content_js)

    return plugin_path


if __name__ == '__main__':
    gen_plugin()
