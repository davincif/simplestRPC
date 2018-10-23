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
	1. [Middleware Command](#mc-middleware-command)
	1. [Error](#er-error)
	1. [Meta Message](#mm-meta-message)


## Terminology
For the context of this documentation, the terms in this section specified shall be interpreted as described for the matter of avoiding any miss-interpretation.

* **Collection** ─ The mathematical concept of collection.
* **Set** ─ Also known as "*collection*".
* **Data** ─ A *collection* of byte describing some raw data. As integers, float numbers, objects, strings... Or anything else that can be put through the network.
* **Message** ─ A *set* of well-structure duly-warped *data* ready to be sent for a peer.
* **Well Structured** ─ Some *set* of *data* formatted as one of the *messages* types supported.
* **Package** ─ A *collection* of one or more *messages*.
* **Job** ─ The execution of one or more functions in order to comply with some request, locally or remotely.
* **Order** ─ A request to execute a job.
* **Request** ─ Also knonw as "*order*".
* **Command** ─ An *order* to be performed right away. Used only to execute internal middleware routines.
* **Information** ─ Just like in any other computer science context, information here comes to be any *set* of *data*, *message*, or *packages* that carries useful stuff to the one who have it.
* **Conversation** ─ The act of spending computer time to exchange information for any desired reason, for as long as the it takes from the first to the last byte sent.

**OBS.:**
1. Every message is a package (just like the mathematical concept of sets).
1. Every message is well formated.
1. Every communication process beggins with a [MM](#mm-meta-message) message.
1. The time spent to process an order did necessarily end at the end of the conversation. The requester may order a job that may be run later, or a job who the requester don't need to know about the end of it (rg.: warnings).


### Message Types:

| Code | Name | Description |
| :------: | :------: | :-------------: |
| [EO](#eo-execution-order) | Execution Order| Command the other end to execute a remote call. |
| [DD](#dd-data-description) | Data Description | Describe the data to be transferred. Eg.: function's argument types and structures. |
| [DT](#dt-data-transfer) | Data Transfer | The data to be transferred. Well structured and well defined. |
| [ST](#sl-status-request) | Status Request | Peer request the health status of the other peer. |
| [SR](#sr-status-response) | Status Response | Peer's health status response to the other peer. |
| [MC](#mc-middleware-command) | Middleware Command | Order to Middleware for performing some work. |
| [ER](#er-error) | Error | Send Error to peer. |
| [WR](#wr-warning) | Warning | Send Warning to peer |
| [MM](#mm-meta-message) | Meta Message | Message containing information about the next message. |


## Header

```
+---------+---------+---------+
|   TYPE  |   SIZE  | CONTENT |
+---------+---------+---------+
| 2 bytes | 2 bytes | <= 64KB |
+---------+---------+---------+
```

#### type
It consistes of a sequence of two characters, one byte each, those caracters must be of the availables at [Message Types](#message-types) table.

The message type, as

#### size
The size, in bytes, of the message content.

#### content
The data.


## Message Details
At this section you'll find an detailed description, with exemples, of each type of message.

#### EO ─ Execution Order

#### DD ─ Data Description

#### DT ─ Data Transfer

#### ST ─ Status Request

#### SR ─ Status Response

#### MC ─ Middleware Command

#### ER ─ Error

#### WR ─ Warning

#### MM ─ Meta Message
This message has a fixed byte size is always the first to initiate a conversation, carrying the byte size of next package to be transferred.
