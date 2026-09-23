from datetime import datetime, timedelta
import logging

DOMAIN = "login_control"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):

    async def handle_refresh_token_clear(call):
        user_id = call.data.get("user_id")
        mode = call.data.get("mode", "all")
        days = call.data.get("days", 90)
        all_users = call.data.get("all_users", False)

        # Determinem quins usuaris processar
        if all_users:
            users = await hass.auth.async_get_users()
        else:
            if not user_id:
                _LOGGER.error(
                    "user_id is required unless all_users is true"
                )
                return

            user = await hass.auth.async_get_user(user_id)

            if user is None:
                _LOGGER.error("User %s not found", user_id)
                return

            users = [user]

        # Mode ALL: comportament original
        if mode == "all":
            for user in users:
                tokens = list(user.refresh_tokens.values())

                for token in tokens:
                    hass.auth.async_remove_refresh_token(token)

            return

        # Mode INACTIVE
        if mode == "inactive":
            cutoff = datetime.now().astimezone() - timedelta(days=days)

            for user in users:
                tokens = list(user.refresh_tokens.values())

                for token in tokens:
                    last_used = token.last_used_at

                    # Si no tenim informació de l'últim ús,
                    # no l'eliminem per seguretat.
                    if last_used is None:
                        continue

                    # Assegurem que comparem datetimes amb timezone
                    if last_used.tzinfo is None:
                        last_used = last_used.astimezone()

                    if last_used < cutoff:
                        hass.auth.async_remove_refresh_token(token)

            return

        _LOGGER.error(
            "Unknown mode '%s'. Valid modes are: all, inactive",
            mode,
        )

    hass.services.async_register(
        DOMAIN,
        "clear_refresh_tokens",
        handle_refresh_token_clear,
    )

    return True

