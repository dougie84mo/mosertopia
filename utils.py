from moser import MoserStatic
import sys

async def non_sync_loop(util_action):
    browser = await MoserStatic.mosertopia_browser()
    page = await MoserStatic.mosertopia_signin()
    await util_action(page)
    await browser.close()


class MoserUtils:
    def __init__(self):
        largv = len(sys.argv)
        print(sys.argv)
        sync_options = {

        }
        non_sync_options = {
            "UpdateModules": lambda: MoserUtils.UpdateModules()
        }
        action_list = {**sync_options, **non_sync_options}
        if largv > 1:
            util_action_id = int(sys.argv[1])
            if util_action_id < len(action_list) - 1:
                util_action = MoserStatic.choosable_str_dict(action_list, "Which function would you like to run?")
            else:
                util_action = action_list[action_list.keys()[util_action_id]]
        else:
            util_action = MoserStatic.choosable_str_dict(action_list, "Which function would you like to run?")

        if util_action in non_sync_options:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(non_sync_loop(non_sync_options[util_action]))
            loop.close()
        elif util_action in sync_options:
            sync_options[util_action]()
        else:
            print("Warning: Something went very wrong!!!!!")

        @staticmethod
        async def UpdateModules():
            print("Working")


if __name__ == '__main__':
    MoserUtils()
