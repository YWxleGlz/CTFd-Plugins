# Unique flags

This plugin allows you to assign flags to a team and detect cheating.

## Installation

1. Copy the plugins to CTFd's plugin folder
2. Create your own challenges
3. Import the team previously generated with the script into the root folder (`team-generator.py`)
4. Import flags into admin interface

## Limitations

- This plugin only works in team mode
- Team names format is mandatory, so you must use the `Team-<letter>-<id>` format. Check the script: `team-generator.py` at the root folder for more information on group generations

## API Reference

### Route: `/admin/unique-flag` (GET method)

```http
  GET /admin/unique-flag
```

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| -         | -    | -           |

**Description:** This route displays the administration page for the "Unique Flags" plugin. It retrieves the information and errors, and loads the challenges from the database to display them in the `admin-import.html` template.

### Route: `/admin/unique-flag` (POST method)

```http
  POST /admin/unique-flag
```

| Parameter | Type     | Description                                                    |
| :-------- | :------- | :------------------------------------------------------------- |
| `content` | `string` | **Required**. The content of the flags to import (CSV Format). |

**Description:** This route handles the import of flags. It calls the `importFlag` function with the content provided in the form, and then displays the information and errors on the administration page.

### Route: `/admin/unique-flag/delete-flags` (POST method)

```http
  POST /admin/unique-flag/delete-flags
```

| Parameter      | Type     | Description                                                                      |
| :------------- | :------- | :------------------------------------------------------------------------------- |
| `challenge_id` | `string` | (Optional) The identifier of the challenge for which to delete the unique flags. |

**Description:** This route deletes the unique flags from the database. If `challenge_id` is provided, it only deletes the unique flags related to this challenge. Otherwise, it deletes all the unique flags.

### Route: `/admin/unique-flag/cheating-monitor` (GET method)

```http
  GET /admin/unique-flag/cheating-monitor
```

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| -         | -    | -           |

**Description:** This route displays the cheater monitoring page, which lists all the cheating teams registered in the database.
