# 1.2.0.2 unstable

This update contains all updates from 1.1.3 to 1.2.0.2
* chat managers methods fix
* getmention fix

## 1.1.7 dev: 
* testcanarybot.__main__: "projects" error fix

* testcanarybot.framework._application._app:
- "tools property" fix
+ setPrivateList(list of int)
+ appendPrivateList(list of int)
+ removeFromPrivateList(list of int)
+ appendMentions(list of mentions)
+ substractMentions(list of mentions)

* testcanarybot.framework._values.global_expressions
+ UPLOADER_DEBUG
+ API_DEBUG
+ MODULE_FAILED_NOMAIN
+ MODULE_FAILED_HANDLERS
+ MODULE_ALREADY
+ MODULE_ISALREADY
+ MODULE_VALID

* testcanarybot.framework._threading: added private mode and phrase commands support
* testcanarybot.framework._library: added private mode; handlers dict structure is changed

* testcanarybot.objects.__init__.libraryModule all attrubutes deleted

* testcanarybot.objects.decocators.ContextManager: added private mode and phrase commands support
* testcanarybot.objects.decocators.priority: added private mode and phrase commands support
* testcanarybot.objects.decocators.event: added private mode and phrase commands support
* testcanarybot.objects.decocators.action: added private mode and phrase commands support

* update docs, .gitignore

* ./library/example-exceptions.py -> ./library/examples-exceptions
* private mode and phrase commands examples

## 1.1.8 dev
* tools:
- system_message -> log
+ send_message(package, message, **kwargs)
+ send_photo(package, assets, **kwargs)
+ send_attachment(package, attachment, **kwargs)
+ send_document(package, assets, **kwargs)

* log: deleted printing handlers dict functions

* tppm:
- support for private_list
- root.py sample is changed
- libraryModule sample is changed

* uploader:
- assets fix

## 1.1.9 dev
### readme
* VK Community blog is removed.
### examples
* assets updated
* exceptions updated
* reactions updated
* uploader updated
### patch
* "framework application app" exception fix
* void fix
* custom mentions fix
### application
* app: deleted methods (appendMentions, substractMentions, appendPrivateList, removeFromPrivateList)
* added param "delete_last" for tools methods (wait_reply, send_reply, send_attachment, send_photo, send_document)
* added tools method "delete_message"

* changed a way to get name of tcb library

* trust_env patch
* Update _library.py

## 1.2.0.1 patch
* added "cbosp" mirror

### patch
* callVoid patch
* patched handler dictionary: if handler registered for commands with similar start, it sorts reverted by word count

## 1.2.0.2 patch
* changed a way to get name of tcb library