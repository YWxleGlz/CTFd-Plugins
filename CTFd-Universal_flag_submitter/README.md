# Universal flag submitter

This plugin lets you create blackbox challenges.

# Installation

1. Copy the plugins to CTFd's plugin folder
2. Create your own challenges
3. Go to the plugin -> blackbox menu, and select the challenges you want to hide.

Done, you can start the CTF

Warning this plugin is not compatible with native requirements & next functions

## Limitation

- This plugin only works in team mode

## API Reference

### Route: `/attempt-hidden-challenge` (POST method)

```http
  POST /attempt-hidden-challenge
```

| Parameter  | Type   | Description                    |
| :--------- | :----- | :----------------------------- |
| submission | string | Flag the user wishes to submit |

**Description:**
This route allows authenticated users to attempt to solve a hidden challenge. It first checks if there are any visible challenges, and for each of them, it calls the `attempt` method of the corresponding challenge class. If the attempt is successful and the player has not already solved this challenge, it adds the solve to the database. Otherwise, it adds a failure.

### Route: `/admin/hide-challenge` (GET method)

```http
  GET /admin/hide-challenge
```

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| -         | -    | -           |

**Description:**
This route displays the administration page for hiding challenges. It retrieves the list of visible challenges and indicates which ones are hidden or not. The information and errors are also displayed.

### Route: `/admin/hide-challenge` (POST method)

```http
  POST /admin/hide-challenge
```

| Parameter    | Type        | Description                        |
| :----------- | :---------- | :--------------------------------- |
| `challenges` | `list[int]` | The list of challenge IDs to hide. |

**Description:**
This route handles the request to hide challenges. It removes the prerequisites from all visible challenges, and then sets the prerequisites for the challenges selected in the form. The changes are then saved to the database, and the challenge cache is cleared.
