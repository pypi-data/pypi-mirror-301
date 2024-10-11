
## CATO-CLI - mutation.container.delete:
[Click here](https://api.catonetworks.com/documentation/#mutation-delete) for documentation on this operation.

### Usage for mutation.container.delete:

`catocli mutation container delete -h`

`catocli mutation container delete <accountID> <json>`

`catocli mutation container delete 12345 "$(cat < delete.json)"`

`catocli mutation container delete 12345 '{"DeleteContainerInput": {"ContainerRefInput": {"by": {"by": "enum(ObjectRefBy)"}, "input": {"input": "String"}}}}'`

#### Operation Arguments for mutation.container.delete ####
`DeleteContainerInput` [DeleteContainerInput] - (required) N/A 
`accountId` [ID] - (required) N/A 
