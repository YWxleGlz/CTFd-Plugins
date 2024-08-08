# Writeup

This plugin lets you add solutions to your challenges.

# Installation

1. Copy the plugins to CTFd's plugin folder
2. Create your own challenges
3. Go to the plugin -> Writeup -> Create your writeup

Done.

It is possible to deactivate the plugin, but the CTFd server must be restarted for the changes to take effect.

# Known issues / Possible improvements

- Issues - In the writeup editing form, the ability to add images is missing (there's a js error). (Issue [#2545](https://github.com/CTFd/CTFd/issues/2545))
- Improvement - Don't reload the page, but rather interact with the API, which would return JSON.

## API Reference

### Route: `/writeup/<int:challenge_id>` (GET method)

```http
  GET /writeup/<int:challenge_id>
```

| Parameter      | Type  | Description                            |
| :------------- | :---- | :------------------------------------- |
| `challenge_id` | `int` | **Required**. The ID of the challenge. |

**Description:**
This route displays the writeup for the specified challenge. If the challenge is unlocked, the writeup content is rendered using the `custom-page.html` template. Otherwise, an error page is rendered.

### Route: `/admin/writeup` (GET method)

```http
  GET /admin/writeup
```

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| -         | -    | -           |

**Description:**
This route displays the administration page for the writeup plugin. It retrieves the information and errors, and checks if the plugin is currently enabled. The page renders the `writeup_config.html` template, which includes the list of challenges and the plugin's configuration.

### Route: `/admin/writeup` (POST method)

```http
  POST /admin/writeup
```

| Parameter        | Type   | Description                                      |
| :--------------- | :----- | :----------------------------------------------- |
| `plugin_enabled` | `bool` | Whether to enable or disable the writeup plugin. |

**Description:**
This route updates the writeup plugin configuration. If the `plugin_enabled` parameter is true, the plugin is enabled; otherwise, the plugin is disabled. A server restart is also required when changing the configuration.

### Route: `/admin/writeup/edit/<int:challenge_id>` (GET method)

```http
  GET /admin/writeup/edit/<int:challenge_id>
```

| Parameter      | Type  | Description                            |
| :------------- | :---- | :------------------------------------- |
| `challenge_id` | `int` | **Required**. The ID of the challenge. |

**Description:**
This route displays the writeup editor for the specified challenge. It retrieves the existing writeup, if any, and the challenge information, and renders the `writeup_editor.html` template.

### Route: `/admin/writeup/edit/<int:challenge_id>` (POST method)

```http
  POST /admin/writeup/edit/<int:challenge_id>
```

| Parameter      | Type     | Description                            |
| :------------- | :------- | :------------------------------------- |
| `challenge_id` | `int`    | **Required**. The ID of the challenge. |
| `description`  | `string` | The new content of the writeup.        |

**Description:**
This route updates the writeup for the specified challenge. If the writeup doesn't exist, a new one is created. Otherwise, the existing writeup is updated with the new content. The changes are then committed to the database.

### Route: `/admin/writeup/delete/<int:challenge_id>` (POST method)

```http
  POST /admin/writeup/delete/<int:challenge_id>
```

| Parameter      | Type  | Description                            |
| :------------- | :---- | :------------------------------------- |
| `challenge_id` | `int` | **Required**. The ID of the challenge. |

**Description:**
This route deletes the writeup for the specified challenge. The writeup is retrieved from the database and then deleted.

### Route: `/admin/writeup/visibility/<int:challenge_id>` (PUT method)

```http
  PUT /admin/writeup/visibility/<int:challenge_id>
```

| Parameter      | Type  | Description                            |
| :------------- | :---- | :------------------------------------- |
| `challenge_id` | `int` | **Required**. The ID of the challenge. |

**Description:**
This route toggles the visibility of the writeup for the specified challenge. It retrieves the writeup from the database and flips the `visible` flag. The updated writeup is then saved to the database.
