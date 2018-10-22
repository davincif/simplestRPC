# Application Protocol

## Index
1. [Terminology](#terminology)
1. [Message types table](#message-types)
1. [Message Details](#message-details)
	1. [Execution Order](#eo-execution-order)
	1. [Data Description](#dd-data-description)
	1. [Data Transfer](#dt-data-transfer)
	1. [Status Solicitation](#sl-status-solicitation)
	1. [Status Response](#sr-status-response)
	1. [Middlewere Command](#mc-middlewere-command)
	1. [Error](#er-error)
	1. [Meta Message](#mm-meta-message)

## Terminology
For the context of this documentation, the terms in this section specified shall be interpreted as described for the matter of avoiding any miss-interpretation.

* **Collection** ─ The mathematical concept of collection. Can also be refered as *Set*.
* **Set** ─ Also known as *Collection*.
* **Data** ─ A *collection* of byte describing some useful raw structure, eg.: integers, float numbers, objects, strings. Or anything else that can be put through the network.
* **Message** ─ A *set* of *data* well structure and duly warped ready to be sent for a peer.
* **Well Structured** ─ Some *set* of *data* formated within one of the *messages* types supported.
*  **Package** ─ A *collection* of one or more *messages*.
* **Order** ─ A solicitation to execute a remote call.
* **Command** ─ A *order* that must be executed right away. Used only to execute internal middlewere routines.
* **Conversation** ─ All the communication involving the exchange of *packages* since the beggining of the requirement until get a final response. It may include one to several chunks of data.

**OBS.:**
1. Every message is a package (just like the mathematical concept of sets).
1. Every message is well formated.
1. Every communication process beggins with a [MM](#mm-meta-message) message.

### Message Types:

| Code | Name | Description |
| :------: | :------: | :-------------: |
| [EO](#eo-execution-order) | Execution Order| Command the other end to execute a remote call. |
| [DD](#dd-data-description) | Data Description | Describe the data to be transferred. Eg.: function's argument types and structures. |
| [DT](#dt-data-transfer) | Data Transfer | The data to be transferred. Well structured and well defined. |
| [SL](#sl-status-solicitation) | Status Solicitation | Peer request the health status of the other peer. |
| [SR](#sr-status-response) | Status Response | Peer's health status response to the other peer. |
| [MC](#mc-middlewere-command) | Middlewere Command | Order to Middlewere for performing some work. |
| [ER](#er-error) | Error | Send Error to peer. |
| [MM](#mm-meta-message) | Meta Message | Message containing information about the next message. |

## Message Details
At this section you'll find an detailed description, with exemples, of each type of message.

#### EO ─ Execution Order

#### DD ─ Data Description

#### DT ─ Data Transfer

#### SL ─ Status Solicitation

#### SR ─ Status Response

#### MC ─ Middlewere Command

#### ER ─ Error

#### MM ─ Meta Message
This message has a fixed byte size is always the first to initiate a conversation, carrying the byte size of next package to be transferred.
