from simple_ledger.cli import db, table, console

values = {
    "str1": "customer_name",
    "str": "customer_mobile",
    "float": "amount_charged",
}


def add_entry():
    console.print("We are now adding a new entry ...")
    inputs = {}
    for val in [
        "customer_name",
        "customer_mobile",
    ]:
        inputs[val] = console.input(
            f"Enter the value for [bold italic underline yellow]{val.replace('_',' ').title()}[/]: "
        )
    for val in ["amount_charged"]:
        inputs[val] = float(
            console.input(
                f"Enter the value for [bold italic underline yellow]{val.replace('_',' ').title()}[/]: "
            )
        )

    return inputs
